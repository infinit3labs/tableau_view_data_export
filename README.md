# Python Tableau Data View Extractor
Python Module to Access Tableau API and Export CSV Data from a View

This module allows an admin user to configure clients to access a Tableau server and choose a view to export to csv.

The separation of permissions requires each client to have a different site on the server and that the client has been notified of the site name.

### Module contents:
* *pub_tableau_api* : this is the main program logic.
* *pub_tableau_api_auth* : this module is to authenticate with the server and obtain a token.  It also retrieves the site ID to use in later calls.  Since this API call requires the site name, it provides an automatic scope to what data is accessible by the script user.
* *pub_tableau_api_get_data* : this module retrieves the csv file of a view and passes it to the writer module to save to disk.
* *pub_tableau_api_get_views* : this module returns a list of all views within a site and allows the user to choose a view for export.
* *pub_tableau_api_urls* : this is a plain dictionary with API urls.

## Version 1.1
* initial release (12 Sept 2019)

## Version 1.2
* allow the user to select filters on the views before export.
