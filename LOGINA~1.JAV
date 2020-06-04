package com.example.androidregisterandlogin;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class LoginActivity extends AppCompatActivity {
    private EditText email , password ;
    private Button btn_login;
    private TextView link_regist;
    private ProgressBar loading;
    private static String URL_LOGIN="http://192.168.43.75/login.php";
    SessionManager sessionManager;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
        sessionManager = new SessionManager(this);
        loading = findViewById(R.id.loading);
        email = findViewById(R.id.email);
        password = findViewById(R.id.password);
        btn_login=findViewById(R.id.btn_login);
        link_regist=findViewById(R.id.link_regist);

        btn_login.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                 String mEmail = email.getText().toString().trim();
                 String mPass = password.getText().toString().trim();
                 if(!mEmail.isEmpty() || !mPass.isEmpty()){
                     Login(mEmail,mPass);
                 }else {
                     email.setError("please insert email");
                     password.setError("please insert password");

                 }
            }
        });
        link_regist.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(LoginActivity.this,MainActivity.class));
            }
        });


    }

    private void Login(final String email , final String password) {
        loading.setVisibility(View.VISIBLE);
        btn_login.setVisibility(View.GONE);

        StringRequest stringRequest = new StringRequest(Request.Method.POST, URL_LOGIN,

                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        try {
                            JSONObject jsonObject=new JSONObject(response);
                            String success = jsonObject.getString("success");
                            JSONArray jsonArray =jsonObject.getJSONArray("login");

                            if(success.equals("1")){
                                for (int i=0 ; i<jsonArray.length();i++)
                                {

                                    JSONObject object = jsonArray.getJSONObject(i);
                                    String name = object.getString("name").trim();
                                    String email = object.getString("email").trim();
                                    String user_check = object.getString("user_check").trim();
                                    String count = object.getString("count").trim();
                                   // String price_each= object.getString("price_each").trim();

                                    String id = object.getString("id").trim();//zawd de

                                    sessionManager.createSession(name,email,id,user_check,count);//zawd de
                                    Intent intent = new Intent(LoginActivity.this,Welcome.class);
                                    Intent intent2=new Intent(LoginActivity.this,usercheck.class);
                                    intent.putExtra("name",name);
                                    intent.putExtra("email",email);
                                    intent2.putExtra("user_check",user_check);
                                    intent2.putExtra("count",count);

                                    startActivity(intent);
                                    finish();
                                    loading.setVisibility(View.GONE);

                                }
                            }
                        } catch (JSONException e) {

                            e.printStackTrace();
                            loading.setVisibility(View.GONE);
                            btn_login.setVisibility(View.VISIBLE);
                            Toast.makeText(LoginActivity.this," Error!"+ e.toString(),Toast.LENGTH_SHORT).show();
                        }

                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        loading.setVisibility(View.GONE);
                        btn_login.setVisibility(View.VISIBLE);

                        Toast.makeText(LoginActivity.this,"Error!"+ error.toString(),Toast.LENGTH_SHORT).show();

                    }
                })

        {
            @Override
            protected Map<String, String> getParams() throws AuthFailureError {
                Map<String,String> params = new HashMap<>();
                params.put("email",email);
                params.put("password",password);
                return params;
            }
        };
        RequestQueue requestQueue = Volley.newRequestQueue(this);
        requestQueue.add(stringRequest);
    }
}
