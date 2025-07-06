package com.example.myproject;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import java.util.HashMap;
import java.util.Map;

public class RegisterActivity extends AppCompatActivity {
    EditText editTextEmail, editTextPassword, editTextName, editTextGender;
    EditText editTextAddress, editTextPhoneNum;
    Button signUp;

    TextView registered, textViewError;

    String name, email, password, gender;
    String address, PhoneNumber;
    ProgressBar progressBar;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);

        editTextEmail = findViewById(R.id.emailText);
        editTextPassword = findViewById(R.id.passwordSignUpText);
        editTextName = findViewById(R.id.nameText);
        editTextAddress = findViewById(R.id.addressText);
        editTextPhoneNum = findViewById(R.id.PhonernumberText);
        signUp = findViewById(R.id.SignUpButton);
        registered = findViewById(R.id.AlreadySignText);
        textViewError = findViewById(R.id.error);
        progressBar = findViewById(R.id.progressBar);
        editTextGender = findViewById(R.id.genderText);

        signUp.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                textViewError.setVisibility(View.GONE);
                progressBar.setVisibility(View.VISIBLE);
                email = String.valueOf(editTextEmail.getText());
                password = String.valueOf(editTextPassword.getText());
                name = String.valueOf(editTextName.getText());
                address = String.valueOf(editTextAddress.getText());
                PhoneNumber = String.valueOf(editTextPhoneNum.getText());
                gender = String.valueOf(editTextGender.getText());

                // 添加日志以确认所有字段已正确填充
                Log.d("RegisterActivity", "email: " + email);
                Log.d("RegisterActivity", "password: " + password);
                Log.d("RegisterActivity", "name: " + name);
                Log.d("RegisterActivity", "address: " + address);
                Log.d("RegisterActivity", "PhoneNumber: " + PhoneNumber);

                RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
                String url = apiURLs.REGISTER;

                StringRequest stringRequest = new StringRequest(Request.Method.POST, url,
                        new Response.Listener<String>() {
                            @Override
                            public void onResponse(String response) {
                                progressBar.setVisibility(View.GONE);
                                if (response.equals("success")) {
                                    Toast.makeText(getApplicationContext(), "Register success!!", Toast.LENGTH_SHORT).show();
                                    Intent intent = new Intent(getApplicationContext(), LoginActivity.class);
                                    startActivity(intent);
                                    finish();
                                } else {
                                    textViewError.setText(response);
                                    textViewError.setVisibility(View.VISIBLE);
                                }
                            }
                        }, new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        progressBar.setVisibility(View.GONE);
                        textViewError.setText(error.getLocalizedMessage());
                        textViewError.setVisibility(View.VISIBLE);
                    }
                }) {
                    @Override
                    protected Map<String, String> getParams() {
                        Map<String, String> paramV = new HashMap<>();
                        paramV.put("username", name);
                        paramV.put("passward", password); // 確保拼寫與後端一致
                        paramV.put("email", email);
                        paramV.put("address", address);
                        paramV.put("Phonenumber", PhoneNumber);
                        paramV.put("gender", gender); // 加入性別參數
                        return paramV;
                    }

                };
                queue.add(stringRequest);
            }
        });

        registered.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(RegisterActivity.this, LoginActivity.class);
                startActivity(intent);
                finish();
            }
        });
    }
}
