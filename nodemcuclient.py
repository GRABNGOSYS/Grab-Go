import socket
import requests
import socket_server
import mysql
price=''      # Global variable that holds the product's price after retrieving it from  (products_table) table
productname=''# Global variable that holds the product's name after retrieving it from  (products_table) table
useridd=''    # Global variable that holds the current customer id after detecting it by face detection

# selectvariblesfromtable function retrieve the product price and name from products_table table in users database
# this function takes 2 variables (tagidd-> the current RFID tag number sent by NodeMCU , useridd-> current customer face detected)

def select_variables_from_table(tagidd,useridd):

        connection = mysql.connector.connect(host='localhost',
                                             database='users',
                                             user='root',
                                             password='root')
        cursor = connection.cursor()
        mySql_insert_query2 = """SELECT product_price,product_name FROM products_table WHERE tag_id= %s"""


        cursor.execute(mySql_insert_query2, (tagidd,))
        myresult = cursor.fetchall() # array hold the  rows retrieved from the "mysql_insert_query2" query
        for x in myresult:           # looping on each retrieved row
           price=x[0]
           productname=x[1]
           print(price)
           print(productname)
        # insert the custumer's id , product name and price  taken by this customer in virtual_cart table
        sql = """INSERT INTO virtual_cart (user_id,user_check,price_each) VALUES (%s, %s, %s)"""
        val = (useridd,productname,price)
        cursor.execute(sql, val)
        connection.commit()

# the socket client function
def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000                  # socket server port number (Note:Port numbers range from 0 to 65535, but only port numbers 0 to 1023 are reserved for privileged services and designated as well-known ports.)

    client_socket = socket.socket()      # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = "test"                     # a default message to keep the connection always on between the client and the server

    while message.lower().strip() != 'bye':

        #client_socket.send(message.encode())  # optional : if client want to send a message to the server
        url = "http://192.168.43.251/"  # ESP's url, ex: https://192.168.102/ (Esp serial prints it when connected to wifi)
        n = requests.get(url)          # get the raw html data in bytes (sends request and warn our esp8266)
        print(n.text + "\n")
        tagidd=n.text                  # the current RFID tag number sent by NodeMCU

        data = client_socket.recv(1024).decode()         # receive response from the server
        #print('Received from server: ' + data)           # show in terminal the message sent by server (current face detected image id )
        indxx = data.rindex('/')                         # this function gets the id of the last '/' sent with the server's message
        current_face_detected= data[indxx + 1:len(data)] # cut the image's id of the current detected customer from packets sent from server
        print(current_face_detected)
        indxses= current_face_detected.rindex('.')       # this function gets the id of the last '.' sent with the server's message
        useridd = current_face_detected[0:indxses]       # cut the current user's id from the image name sent from the server
        print(useridd)

        select_variables_from_table(tagidd,useridd)       # call the select_variables_from_table function by current tagidd and useridd




#client_socket.close()  # close the connection

#calling client function to start the server-client connection
if __name__ == '__main__':
    client_program()