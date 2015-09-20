package ca.uwaterloo.etxt;

import android.content.ContentResolver;
import android.database.Cursor;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Typeface;
import android.net.Uri;
import android.os.Handler;
import android.support.v4.app.Fragment;
import android.os.Bundle;
import android.text.Editable;
import android.text.Html;
import android.text.TextWatcher;
import android.text.style.UnderlineSpan;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.Timer;
import java.util.TimerTask;


/**
 * A placeholder fragment containing a simple view.
 */
public class MainActivityFragment extends Fragment implements AdapterView.OnItemClickListener{

    private static MainActivityFragment inst;
    ArrayList<String> smsMessagesList = new ArrayList<String>();
    ListView smsListView;
    ArrayAdapter arrayAdapter;

    public static MainActivityFragment instance() {
        return inst;
    }

    @Override
    public void onStart() {
        super.onStart();
        inst = this;
    }

    // EditText Object
    private static EditText receiverET;
    private static EditText subjectET;
    private static EditText messageET;

    public MainActivityFragment() {
    }


    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        final View rootView = inflater.inflate(R.layout.fragment_main, container, false);

        smsListView = (ListView) rootView.findViewById(R.id.SMSList);
        arrayAdapter = new ArrayAdapter<String>(getActivity(), android.R.layout.simple_list_item_1, smsMessagesList);
        smsListView.setAdapter(arrayAdapter);
        smsListView.setOnItemClickListener(this);
        refreshSmsInbox();

        // Initialize EditText Object
        receiverET = (EditText)rootView.findViewById(R.id.receiver);
        subjectET = (EditText)rootView.findViewById(R.id.subject);
        messageET = (EditText)rootView.findViewById(R.id.message);

        return rootView;
    }

    public static String getText() {
        // Split multiple receivers
        String[] receivers = receiverET.getText().toString().split(",");
        String subject = subjectET.getText().toString();
        String message = messageET.getText().toString();

        // If there is no receiver
        if (receivers[0].equals("")) {
            return "No Receiver";
        } else {
            for (String s : receivers) {
                if (!s.contains("@") && !s.contains(".")) {
                    return "Invalid Receiver";
                }
            }
        }
        if (subject.equals("")) {
            return "No Subject";
        } else if (message.equals("")) {
            return "No Message";
        }

        // Parse message to a giant string
        String textMessage = "";
        for (String receiver : receivers) {
            // Replace any space in the string
            textMessage += receiver + " ";
        }
        textMessage += "\n" + subject;
        textMessage += "\n" + message;

        // Return
        return textMessage;
    }


    @Override
    public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
        try {
            String[] smsMessages = smsMessagesList.get(position).split("\n");
            String address = smsMessages[0];
            String smsMessage = "";
            for (int i = 1; i < smsMessages.length; ++i) {
                smsMessage += smsMessages[i];
            }

            String smsMessageStr = address + "\n";
            smsMessageStr += smsMessage;
            Toast.makeText(getActivity(), smsMessageStr, Toast.LENGTH_SHORT).show();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void refreshSmsInbox() {
        ContentResolver contentResolver = getActivity().getContentResolver();
        Cursor smsInboxCursor = contentResolver.query(Uri.parse("content://sms/inbox"), null, null, null, null);
        int indexBody = smsInboxCursor.getColumnIndex("body");
        int indexAddress = smsInboxCursor.getColumnIndex("address");
        if (indexBody < 0 || !smsInboxCursor.moveToFirst()) return;
        arrayAdapter.clear();
        do {
            if (smsInboxCursor.getString(indexAddress).equals("+16473603583")) {
                String str = smsInboxCursor.getString(indexBody).substring(39,smsInboxCursor.getString(indexBody).length()) + "\n";
                arrayAdapter.add(str);
            }
        } while (smsInboxCursor.moveToNext());
    }

    public void updateList(final String smsMessage) {
        arrayAdapter.insert(smsMessage, 0);
        arrayAdapter.notifyDataSetChanged();
    }
}
