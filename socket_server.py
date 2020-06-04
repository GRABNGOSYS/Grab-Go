import face_recognition
import cv2
import numpy as np
import requests
from requests.exceptions import Timeout
import socket
import mysql.connector
from mysql.connector import Error

def server_program():

    host = socket.gethostname()     # get the hostname
    port = 5000                     # initiate port no above 1024
    detected_user_name = ''

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))

    while True:

        # receive data stream. it won't accept data packet greater than 1024 bytes
        # data2 = conn.recv(1024).decode()
        # print("from connected user: " + str(data))
        ############################################ GET USER'S IMAGE FROM DATABASE ################################
        photop = [] # array saves names of the user's images retrieved from the database
        try:
            connection = mysql.connector.connect(host='localhost',
                                                 database='users',
                                                 user='root',
                                                 password='root')

            sql_select_Query = "SELECT photopath FROM users_table " # retrieving the names of the user's image from the "users_table" table
            cursor = connection.cursor()
            cursor.execute(sql_select_Query)
            records = cursor.fetchall()                            # array saves the retrieve raws from the "sql_select_Query" query
            print(cursor.rowcount)                                 # .rowcount gets the number of rows retrieved from the table
            for x in records:
                photop.append(x[0])                                # save the retrieved data in photop array
        except Error as e:
            print("Error reading data from MySQL table", e)
        finally:
            if (connection.is_connected()):
                connection.close()
                cursor.close()
                print("MySQL connection is closed")
        print(photop)

        known_face_encodings = []
        known_face_names = []
        for x in photop:
            forphoto = "images\\" + x   # adding the path of the saved images to the names of the images
            print(forphoto)
            known_face_encodings.append(face_recognition.face_encodings(face_recognition.load_image_file(forphoto))[0]) # appending  the known faces to known_face_encodings array
            known_face_names.append(x)                                                                                  # appending  the names of the known faces to known_face_names array

        ############################################ GET USER'S IMAGE FROM DATABASE ################################

       ############################################# APPLY FACE DETECTION AND RECOGNITION ON THE TAKEN FRAMES FROM THE LIVE STREAMING #############################################
        video_capture = cv2.VideoCapture(0)

        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True

        while True:

            ret, frame = video_capture.read()

            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            rgb_small_frame = small_frame[:, :, ::-1]

            if process_this_frame:
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"

                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                        #if(name!=detected_user_name): # condition to handle sending the same frame name too much to the client side
                        detected_user_name=name
                        data="/"+detected_user_name # to separate the  frames sent to the client
                        conn.send(data.encode())  # send current face detected user's image name to the client


                    face_names.append(name)

            process_this_frame = not process_this_frame


            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'): # when q is clicked the server will refresh and start allover again to allow newly added user's images to be added to the face detection code
                break

        video_capture.release()
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    #conn.close()  # close the connection

       ############################################# APPLY FACE DETECTION AND RECOGNITION ON THE TAKEN FRAMES FROM THE LIVE STREAMING #############################################



if __name__ == '__main__':
    server_program()