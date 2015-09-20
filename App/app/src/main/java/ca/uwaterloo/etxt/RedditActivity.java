package ca.uwaterloo.etxt;

import android.content.Context;
import android.support.v7.app.ActionBarActivity;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.telephony.SmsManager;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import java.util.ArrayList;

public class RedditActivity extends ActionBarActivity {

    Toast toast;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_reddit);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        switch(id) {
            case R.id.action_send:
                sendMessage();
                break;
        }

        return super.onOptionsItemSelected(item);
    }



    private void sendMessage(){
        String a = ((TextView)findViewById(R.id.raybae)).getText().toString();
        if(a.equals("")){
            showToast("Enter something bro");
        }else{


            try {
                SmsManager smsManager = SmsManager.getDefault();
                String[] brokenString = chopString(a);
                for (int i = 0; i < brokenString.length; i++) {
                    Log.e("HO", brokenString[i]);
                    smsManager.sendTextMessage("+16473603583", null, brokenString[i]
                            , null, null);
                }
                showToast("Text Sent");
            } catch (Exception e) {
                showToast("Text Failed To Send");
                e.printStackTrace();
            }
        }
    }

    private void showToast(String s) {
        if (toast == null) {
            toast = Toast.makeText(this,s,Toast.LENGTH_SHORT);
            toast.show();
        }
        toast.setText(s);
        toast.setDuration(Toast.LENGTH_SHORT);
        toast.show();
    }

    private String[] chopString(String message) {
        if (message.length() <= 1550) return new String[] { message };
        else {
            String[] chop = new String[message.length() / 1550 + 1];
            int counter = 0;
            while (message.length() > 1550) {
                chop[counter] = message.substring(0,1551);
                message = message.substring(1551,message.length());
                counter++;
            }
            chop[counter] = message;
            return chop;
        }
    }

}
