package com.example.rc_car_final;

import static com.example.rc_car_final.MainActivity.get_ip;
import static com.example.rc_car_final.MainActivity2.IP;
import static com.example.rc_car_final.MainActivity2.down_flag_pressed;
import static com.example.rc_car_final.MainActivity2.down_flag_released;
import static com.example.rc_car_final.MainActivity2.exit_flag;
import static com.example.rc_car_final.MainActivity2.left_flag_pressed;
import static com.example.rc_car_final.MainActivity2.left_flag_released;
import static com.example.rc_car_final.MainActivity2.port_num;
import static com.example.rc_car_final.MainActivity2.right_flag_pressed;
import static com.example.rc_car_final.MainActivity2.right_flag_released;
import static com.example.rc_car_final.MainActivity2.setLCD;
import static com.example.rc_car_final.MainActivity2.up_flag_pressed;
import static com.example.rc_car_final.MainActivity2.up_flag_released;
import static com.example.rc_car_final.Thread1.client;
import static com.example.rc_car_final.Thread1.printwriter;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import android.app.Service;
import android.content.Intent;
import android.os.Bundle;
import android.os.IBinder;
import android.provider.Settings;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import java.io.IOException;
import java.io.PrintWriter;
import java.net.Socket;



public class MainActivity2 extends AppCompatActivity {
    static TextView LCD;
    Button button;
    Button UP;
    Button DOWN;
    Button LEFT;
    Button RIGHT;
    Button Maps;
    static boolean up_flag_pressed =false;
    static boolean down_flag_pressed =false;
    static boolean right_flag_pressed =false;
    static boolean left_flag_pressed =false;
    static boolean down_flag_released =false;
    static boolean up_flag_released =false;
    static boolean right_flag_released =false;
    static boolean left_flag_released =false;
    static boolean exit_flag= false;

    static String IP ;
    static String port_num = "4445";
    String msg;
    Thread Thread1 = null;

    @Override
    protected void onStop() {
        super.onStop();
        System.out.println("da5alt");
        exit_flag = true;

        finish();
    }
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main2);
        UP = findViewById(R.id.UP);
        DOWN = findViewById(R.id.DOWN);
        RIGHT = findViewById(R.id.right);
        LEFT = findViewById(R.id.left);
        Maps = findViewById(R.id.Location);
        LCD = findViewById(R.id.textView3);
        IP=get_ip();

        Thread1 = new Thread(new Thread1());
        Thread1.start();

        Maps.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent Map_intent;
                Map_intent = new Intent(getApplicationContext(), MapsActivity.class);
                startActivity(Map_intent);
            }
        });
//        try {
//            client = new Socket(IP, Integer.parseInt(port_num));
//            printwriter = new PrintWriter(client.getOutputStream(),true);
//        } catch (IOException e) {
//            e.printStackTrace();
//        }

        View.OnTouchListener handleTouch = new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                Button b = (Button) v;
                String msg;

                switch (event.getAction()) {
                    case MotionEvent.ACTION_DOWN:
                       // System.out.println(b.getText());
                        if( b.getText().equals("D")){
                            down_flag_pressed=true;
                        }
                        if( b.getText().equals("U")){
                            up_flag_pressed=true;
                        }
                        if( b.getText().equals("R")){
                            right_flag_pressed=true;
                        }
                        if( b.getText().equals("L")){
                            left_flag_pressed=true;
                        }
//                        msg = (String) b.getText() + "DOWN";
//                        try {
////                            new Thread(new connect(IP , "4445",msg)).start();
//
//                        }
//                        catch (IOException e) {
//                            setLCD(e.toString());
//                        }
//                        printwriter.write(msg);
//                        printwriter.flush();
                        break;
                    case MotionEvent.ACTION_UP:
                        if(b.getText().equals("D")){
                            down_flag_released=true;
                            down_flag_pressed=false;

                        }
                        if( b.getText().equals("U")){
                            up_flag_released=true;
                            up_flag_pressed=false;

                        }
                        if( b.getText().equals("R")){
                            right_flag_released=true;
                            right_flag_pressed=false;

                        }
                        if( b.getText().equals("L")){
                            left_flag_released=true;
                            left_flag_pressed=false;

                        }
//                         msg = (String) b.getText() + "UP";
//                        try {
//                            new Thread(new connect(IP , "4445",msg)).start();}
//                        catch (IOException e)
//                        {
//                            setLCD(e.toString());
//                        }

                        break;
                }

                return true;
            }
        };
        UP.setOnTouchListener(handleTouch);
        DOWN.setOnTouchListener(handleTouch);
        RIGHT.setOnTouchListener(handleTouch);
        LEFT.setOnTouchListener(handleTouch);
    }
    public static void setLCD(String s){
            LCD.setText(s);
        }
}

class connect implements Runnable {
    private Socket client;
    private PrintWriter printwriter;
    String ip;
    String port_num;
    String msg;


    connect(String ip,String port_num,String msg) throws IOException {
        this.ip=ip;
        this.port_num=port_num;
        this.msg=msg;
    }
    @Override
    public void run() {
        try {
            client = new Socket(ip, Integer.parseInt(port_num));
            printwriter = new PrintWriter(client.getOutputStream(),true);
            printwriter.write(msg);
            printwriter.flush();
            //closing the serial
            printwriter.close();
            // closing the connection
            client.close();
        }
        catch (IOException e)
        {
            setLCD(e.toString());
        }
        catch (Exception e)
        {
            setLCD(e.toString());

        }

    }
}

class Thread1 implements Runnable {
    static Socket client;
    static PrintWriter printwriter;
    String msg = "First";

    //for test
    int counter =0;

    @Override
    public void run() {
        try {
            client = new Socket(IP, Integer.parseInt(port_num));
            printwriter = new PrintWriter(client.getOutputStream(), true);
            while (true) {
                if(exit_flag){
                    printwriter.write("exit");
                    printwriter.flush();
                    //closing the serial
                    printwriter.close();
                    // closing the connection
                    client.close();
                }
                if (down_flag_released){
                    msg = "D"+ "UP";
                    down_flag_pressed=false;
                    down_flag_released=false;
                }
                if (up_flag_released){
                    msg = "U"+ "UP";
                    up_flag_pressed=false;
                    up_flag_released=false;
                }
                if (right_flag_released){
                    msg = "R"+ "UP";
                    right_flag_pressed=false;
                    right_flag_released=false;
                }
                if (left_flag_released){
                    msg = "L"+ "UP";
                    left_flag_pressed=false;
                    left_flag_released=false;
                }
                if (down_flag_pressed){
                    msg = "D"+ "DOWN";
                    down_flag_pressed=false;

                }
                if (up_flag_pressed){
                    msg = "U"+ "DOWN";
                    up_flag_pressed=false;

                }
                if (right_flag_pressed){
                    msg = "R"+ "DOWN";
                    right_flag_pressed=false;

                }
                if (left_flag_pressed){
                    msg = "L"+ "DOWN";
                    left_flag_pressed=false;

                }
                if (msg != "D" ) {
                    System.out.println(msg);
                    printwriter.write(msg);
                    printwriter.flush();
                    msg="D";
                }

            }
//            printwriter.write(msg);
//            printwriter.flush();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

