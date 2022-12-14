## Sample ShareX configuration

````json
{
  "Version": "14.1.0",
  "DestinationType": "URLShortener",
  "RequestMethod": "POST",
  "RequestURL": "https://my.tld/create",
  "Headers": {
    "authorization": "my-authorization-key"
  },
  "Body": "MultipartFormData",
  "Arguments": {
    "url": "{input}"
  },
  "URL": "https://my.tld/{json:code}",
  "ThumbnailURL": "",
  "DeletionURL": "",
  "ErrorMessage": ""
}
````

*Some valued need to be changed!*

also in [this file](/other/sharex.sxcu)
