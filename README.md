A python script that exports scrobbles from last.fm

The scrobbles are put into a json file and sorted in such a way as to minimize the file size.

List of available commands:

<dl>
  <dt>start over</dt>
  <dd>Fetches all tracks listened by a given user. The output is put into a json file.</dd>
  <dt>update</dt>
  <dd>Updates the json file given by the user. Tracks are only added from the 'last track' timestamp. Previous tracks are not touched.</dd>
  <dt>change settings</dt>
  <dd>Allows the user to change their settings. Which consist of the username(not recommended changing) and the json filename.</dd>
  <dt>username</dt>
  <dd>Shows the current username.</dd>
  <dt>filename</dt>
  <dd>Shows the current filename.</dd>
  <dt>change api</dt>
  <dd>Allows the user to change the api key used by the script.</dd>
</dl>
