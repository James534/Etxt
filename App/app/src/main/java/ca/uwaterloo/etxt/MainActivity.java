package ca.uwaterloo.etxt;

import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.telephony.SmsManager;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.Toast;


public class MainActivity extends ActionBarActivity {

    Toast toast;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();

        switch(id) {
            case R.id.action_send:
                sendTextMessage();
                break;
        }
        return super.onOptionsItemSelected(item);
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

    private void sendTextMessage() {
        String message = MainActivityFragment.getText();
        switch (message) {
            case "No Receiver":
                showToast("No Receiver");
                return;
            case "No Subject":
                showToast("No Subject");
                return;
            case "No Message":
                showToast("No Message");
                return;
            case "Invalid Receiver":
                showToast("Invalid Receiver");
                return;
        }

        try {
            SmsManager smsManager = SmsManager.getDefault();
            String[] brokenString = chopString(message);
            for (int i = 0; i < brokenString.length; i++) {
                Log.e("HO",brokenString[i]);
                smsManager.sendTextMessage("+16473603583", null, brokenString[i]
                        , null, null);
            }
            showToast("Text Sent");
        } catch (Exception e) {
            showToast("Text Failed To Send");
            e.printStackTrace();
        }
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
