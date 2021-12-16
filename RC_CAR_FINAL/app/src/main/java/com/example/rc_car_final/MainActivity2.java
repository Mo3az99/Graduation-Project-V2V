package com.example.rc_car_final;

import static com.example.rc_car_final.MainActivity.get_ip;
import static com.example.rc_car_final.MainActivity2.setLCD;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

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




    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main2);


//        button = findViewById(R.id.button);
        UP = findViewById(R.id.UP);
        DOWN = findViewById(R.id.DOWN);
        RIGHT = findViewById(R.id.right);
        LEFT = findViewById(R.id.left);

        LCD = findViewById(R.id.textView3);

        String IP=get_ip();
//        button.setOnClickListener(v -> {
////                LCD.setText("Connected with IP "+get_ip());
//            try {
//                new Thread(new connect(IP , "4445","hamada")).start();}
//            catch (IOException e) {
//                setLCD(e.toString());
//            }
//
//        });


        View.OnTouchListener handleTouch = new View.OnTouchListener() {


            @Override
            public boolean onTouch(View v, MotionEvent event) {
                Button b = (Button) v;
                String msg;

                switch (event.getAction()) {
                    case MotionEvent.ACTION_DOWN:
                        msg = (String) b.getText() + "DOWN";
                        try {
                            new Thread(new connect(IP , "4445",msg)).start();
                        }
                        catch (IOException e) {
                            setLCD(e.toString());
                        }

                        break;
                    case MotionEvent.ACTION_UP:
                         msg = (String) b.getText() + "UP";
                        try {
                            new Thread(new connect(IP , "4445",msg)).start();}
                        catch (IOException e)
                        {
                            setLCD(e.toString());
                        }

                        break;
                }

                return true;
            }
        };
        UP.setOnTouchListener(handleTouch);
        DOWN.setOnTouchListener(handleTouch);
        RIGHT.setOnTouchListener(handleTouch);
        LEFT.setOnTouchListener(handleTouch);

//
////DOWN KEY
//        View.OnTouchListener handleDOWNTouch = new View.OnTouchListener() {
//
//
//            @Override
//            public boolean onTouch(View v, MotionEvent event) {
//                switch (event.getAction()) {
//                    case MotionEvent.ACTION_DOWN:
//
//                        try {
//                            new Thread(new connect(IP, "4445","DOWNDOWN")).start();
//                            Button b2= (Button) v;
//                            setLCD((String) b2.getText());
//                        } catch (IOException e) {
//                            setLCD(e.toString());
//                        }
//
//                        break;
//                    case MotionEvent.ACTION_UP:
//                        try {
//                            new Thread(new connect(IP, "4445","DOWNUP")).start();} catch (IOException e) {
//                            setLCD(e.toString());
//                        }
//
//                        break;
//                }
//
//                return true;
//            }
//        };
//        DOWN.setOnTouchListener(handleDOWNTouch);

//right KEY
//        View.OnTouchListener handleRIGHTTouch = new View.OnTouchListener() {
//
//
//            @Override
//            public boolean onTouch(View v, MotionEvent event) {
//                switch (event.getAction()) {
//                    case MotionEvent.ACTION_DOWN:
//
//                        try {
//                            new Thread(new connect(IP, "4445","RIGHTDOWN")).start();} catch (IOException e) {
//                            setLCD(e.toString());
//                        }
//
//                        break;
//                    case MotionEvent.ACTION_UP:
//                        try {
//                            new Thread(new connect(IP, "4445","RIGHTUP")).start();} catch (IOException e) {
//                            setLCD(e.toString());
//                        }
//
//                        break;
//                }
//
//                return true;
//            }
//        };
//        RIGHT.setOnTouchListener(handleRIGHTTouch);

//LEFT KEY
//        View.OnTouchListener handleLEFTTouch = new View.OnTouchListener() {
//
//
//            @Override
//            public boolean onTouch(View v, MotionEvent event) {
//                switch (event.getAction()) {
//                    case MotionEvent.ACTION_DOWN:
//
//                        try {
//                            new Thread(new connect(IP, "4445","LEFTDOWN")).start();} catch (IOException e) {
//                            setLCD(e.toString());
//                        }
//
//                        break;
//                    case MotionEvent.ACTION_UP:
//                        try {
//                            new Thread(new connect(IP , "4445","LEFTUP")).start();} catch (IOException e) {
//                            setLCD(e.toString());
//                        }
//
//                        break;
//                }
//
//                return true;
//            }
//        };
//        LEFT.setOnTouchListener(handleLEFTTouch);

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