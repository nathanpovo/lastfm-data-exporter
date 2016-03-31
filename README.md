# Lastfm Data Exporter

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](http://www.apache.org/licenses/LICENSE-2.0)

__Disclaimer:__ _Only tested on Windows._

### Description
A python script that exports scrobbles from last.fm

The scrobbles are stored in a json file and structured in such a way as to minimize the file size.

### Requirements
Python 3 (or higher)

#### List of available commands:

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
