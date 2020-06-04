package com.example.androidregisterandlogin;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import java.util.HashMap;

public class Welcome extends AppCompatActivity {
    private TextView name , email ;
    SessionManager sessionManager;
    private Button btn_logout,btn_check;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_welcome);
        sessionManager=new SessionManager(this);
        sessionManager.checkLogin();

        name=findViewById(R.id.name);
        email=findViewById(R.id.email);
        btn_check=findViewById(R.id.btn_check);
        HashMap<String,String> user = sessionManager.getUserDetail();
        String mName = user.get(sessionManager.NAME);
        String mEmail = user.get(sessionManager.EMAIL);
        name.setText(mName);
        email.setText(mEmail);
        btn_logout=findViewById(R.id.btn_logout);
        btn_check.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent2=new Intent(Welcome.this,usercheck.class);
                startActivity(intent2);
            }
        });
        btn_logout.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                sessionManager.logout();
            }
        });




    }
}
