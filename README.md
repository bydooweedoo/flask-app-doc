# flask-app-doc

Quick use
=========

Replace in views.py

	from yourapp import __app__

by

	from myapp import app as __app__

and add in your app.py

    	from doc.views import __documentation__
    	__app__.register_blueprint(__documentation__)