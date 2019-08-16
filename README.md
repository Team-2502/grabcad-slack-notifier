#grabcad-slack-notifier

A hacky solution to put GrabCAD notifications in Slack. Supposed to run on heroku.


## How does it work?

![flowchart of how it works](https://i.imgur.com/kdjdptL.png)

1. GrabCAD sends an email to a Gmail account.  You can turn on emails in the user settings.

1. A Google Apps Script forwards all GrabCAD emails to `trigger@applet.ifttt.com` (it is essentially 
impossible to use Gmail filters to forward emails to IFTTT). Script setup instructions below. 

1. An IFTTT applet takes the GrabCAD emails, and then sends the BodyHTML as raw text to the `grabcad-slack-notifier`

1. `grabcad-slack-notifier` does its best to parse out the comment/file changes from the email HTML

1. `grabcad-slack-notifier` figures out what should be sent in Slack, and then makes a `POST` request to another IFTTT 
applet, with what should be sent in slack under the key `value1` in the JSON payload 

1. This separate IFTTT applet takes `value1` and finally sends it to Slack

### Why so many moving parts?

You could cut out the last step if you could get `grabcad-slack-notifier` to directly send the text to 
Slack, if you had some kind of admin privileges on the workspace. Sadly, the author at the time did not, so 
IFTTT nonsense had to suffice.

### Google Apps Script 

```javascript
function autoForward() {
  var label = 'GrabCAD';
  var recipient = 'trigger@applet.ifttt.com';
  var interval = 1;          //  if the script runs every minute; change otherwise
  var date = new Date();
  var timeFrom = Math.floor(date.valueOf()/1000) - 60 * interval; // find what time it was a minute ago
  var threads = GmailApp.search('label:' + label + ' after:' + timeFrom); // search for emails with appropriate label, came after a minute ago
  for (var i = 0; i < threads.length; i++) {
    var messages = threads[i].getMessages();
    messages[messages.length - 1].forward(recipient);  // forward the last 
  }
}
```

You can go to the [Google Apps Script Website](https://www.google.com/script/start/) to set up this script. Make sure to
[set a trigger](https://developers.google.com/apps-script/guides/triggers/installable#managing_triggers_manually) so that
it runs every minute. 

[source: stackexchange](https://webapps.stackexchange.com/a/95930)     

### for talon members performing maintenance

IFTTT, Heroku, and GrabCAD accounts are under `info@team2502.com`. 
The passwords for the accounts are under the drafts of that Gmail account. Make sure that `info@team2502.com` is added
to all GrabCAD projects that you want to be updated in Slack (`#cad-updates`)