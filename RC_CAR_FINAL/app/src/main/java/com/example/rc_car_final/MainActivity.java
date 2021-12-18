package com.example.rc_car_final;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {
    Button connect_button;
    static EditText car_ip;
    TextView LCD;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        connect_button = findViewById(R.id.connect_button);
        car_ip = findViewById(R.id.car_ip);
        LCD = findViewById(R.id.lcd);
        connect_button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                LCD.setText("Connected with IP " + get_ip());
                Intent intent = new Intent(MainActivity.this, MainActivity2.class);
                startActivity(intent);
            }
        });
    }

    public static String get_ip(){
        String ip = car_ip.getText().toString();

        return ip;
    }

}