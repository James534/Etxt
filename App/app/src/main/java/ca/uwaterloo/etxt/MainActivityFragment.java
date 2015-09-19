package ca.uwaterloo.etxt;

import android.support.v4.app.Fragment;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.EditText;


/**
 * A placeholder fragment containing a simple view.
 */
public class MainActivityFragment extends Fragment {

    // EditText Object
    private static EditText receiverET;
    private static EditText subjectET;
    private static EditText messageET;

    // String Object
    private static String[] receivers;
    private static String subject;
    private static String message;

    public MainActivityFragment() {
    }


    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        final View rootView = inflater.inflate(R.layout.fragment_main, container, false);

        // Initialize EditText Object
        receiverET = (EditText)rootView.findViewById(R.id.receiver);
        subjectET = (EditText)rootView.findViewById(R.id.subject);
        messageET = (EditText)rootView.findViewById(R.id.message);

        return rootView;
    }

    public static String getText() {
        // Split multiple receivers
        receivers = receiverET.getText().toString().split(",");
        subject = subjectET.getText().toString();
        message = messageET.getText().toString();

        // Parse message to a giant string
        String textMessage = "To: ";
        for (int i = 0; i < receivers.length; i++) {
            // Replace any space in the string
            textMessage += receivers[i] + " ";
        }
        textMessage += "\nSubject: " + subject;
        textMessage += "\nMessage: " + message;

        // Return
        return textMessage;
    }
}
