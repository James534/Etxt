package ca.uwaterloo.etxt;

import android.content.ContentResolver;
import android.content.Context;
import android.database.Cursor;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Typeface;
import android.net.Uri;
import android.os.Handler;
import android.support.v4.app.Fragment;
import android.os.Bundle;
import android.telephony.SmsManager;
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
public class RedditActivityFragment extends Fragment{

    ItemAdapter adapter;
    private static RedditActivityFragment inst;
    ListView smsListView;
    ArrayList<Item> items = new ArrayList<Item>();
    int counter = 0;

    public static RedditActivityFragment instance() {
        return inst;
    }

    @Override
    public void onStart() {
        super.onStart();
        inst = this;
    }

    // EditText Objec

    public RedditActivityFragment() {
    }


    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        final View rootView = inflater.inflate(R.layout.fragment_reddit, container, false);

        smsListView = (ListView) rootView.findViewById(R.id.redditlist);
        adapter = new ItemAdapter(getActivity(),items);
        refreshSmsInbox();

        return rootView;
    }

    public void updateList(final String smsMessage) {
        String[] message = smsMessage.split("\n");
        for(String a : message){
            if(a.length()>0&&Character.isDigit(a.charAt(0))){
                items.add(new Item( a.substring(0, a.indexOf(" ")),counter + a.substring(a.indexOf(" "),a.length()-3)));
                counter++;
            }
        }
        ListView listView = (ListView) smsListView.findViewById(R.id.redditlist);
        listView.setAdapter(adapter);
        adapter.notifyDataSetChanged();
    }
    public class ItemAdapter extends ArrayAdapter<Item> {
        public ItemAdapter(Context context, ArrayList<Item> users) {
            super(context, 0, users);
        }

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {
            // Get the data item for this position
            final Item item = getItem(position);
            // Check if an existing view is being reused, otherwise inflate the view
            if (convertView == null) {
                convertView = LayoutInflater.from(getContext()).inflate(R.layout.items, parent, false);
            }
            // Lookup view for data population
            TextView tvName = (TextView) convertView.findViewById(R.id.jimji);
            // Populate the data into the template view using the data object
            tvName.setText(item.value);
            convertView.setOnClickListener(
                    new View.OnClickListener() {
                        @Override
                        public void onClick(View v) {
                            Log.d("Here is what is clicked",item.id);
                        }
                    }
            );
            // Return the completed view to render on screen
            return convertView;
        }
    }
    private class Item{
        String id;
        String value;
        public Item(String a, String b){
            id = a;
            value = b;
        }
    }

    public void refreshSmsInbox() {
        ContentResolver contentResolver = getActivity().getContentResolver();
        Cursor smsInboxCursor = contentResolver.query(Uri.parse("content://sms/inbox"), null, null, null, null);
        int indexBody = smsInboxCursor.getColumnIndex("body");
        int indexAddress = smsInboxCursor.getColumnIndex("address");
        if (indexBody < 0 || !smsInboxCursor.moveToFirst()) return;
        do {
            if (smsInboxCursor.getString(indexAddress).equals("+16473603583")) {
                String from = smsInboxCursor.getString(indexBody).substring(39,smsInboxCursor.getString(indexBody).length());
                String[] parts = from.split("\n");
                String str = "";
                if (parts.length > 2) {
                    str += "From: " + parts[0] + "\n";
                    str += "Subject: " + parts[1];
                    str += smsInboxCursor.getString(indexBody).substring(39 + parts[0].length() + parts[1].length(),smsInboxCursor.getString(indexBody).length());
                    updateList(str);
                }

            }
        } while (smsInboxCursor.moveToNext());
    }
}
