package com.example.androidregisterandlogin;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import java.util.HashMap;

public class usercheck extends AppCompatActivity {

    private TextView user_check,count  ;
    SessionManager sessionManager;
    private Button btn_logout;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_usercheck);
        sessionManager=new SessionManager(this);
        sessionManager.checkLogin();

        user_check=findViewById(R.id.user_check);
        count=findViewById(R.id.count);
        HashMap<String,String> user = sessionManager.getUserDetail();
        String mName = user.get(sessionManager.USER_CHECK);
        String mcount=user.get(sessionManager.COUNT);
        user_check.setText(mName);
        count.setText(mcount);
        btn_logout=findViewById(R.id.btn_logout);
        btn_logout.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                sessionManager.logout();
            }
        });




    }
}
