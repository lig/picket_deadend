Copyright 2008-2010 Serge Matveenko

This file is part of Picket.

Picket is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Picket is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Picket.  If not, see <http://www.gnu.org/licenses/>.

----

## Picket Bugtracker resources

<http://sourceforge.net/projects/picket>

<http://github.com/lig/picket>

<http://www.ohloh.net/p/picket>

<http://picket.nophp.ru/>


## Short installation instructions

1. Install [Python 2.x](http://python.org/).

2. Install [MongoDB](http://www.mongodb.org/).

3. Checkout latest version of Picket from Git repository located here:

    <http://sourceforge.net/scm/?type=git&group_id=210642>
    
    and here:
    
    <http://github.com/lig/picket>
    
    or download latest Picket version here:
    
    <http://picket.nophp.ru/pages/download/>

4. Change working directory to the root directory of your local Picket copy.

5. Copy file "settings/local_sample.py" to "settings/local.py" and edit it to
provide db connection information (sqlite3 good for quick testing).

6. Look for other Picket requirements in "requirements.pip" file compatible
with "pip install -r" command. The main are: Django and mongoengine.

7. Run in terminal to start picket test web server:
$ ./manage.py runserver

8. Point your browser at:
http://localhost:8000/

You are done!

## Bugs, suggestions and other issues

Feel free to report any bugs here:

<http://github.com/lig/picket/issues>
