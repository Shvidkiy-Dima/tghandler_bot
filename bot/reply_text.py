from django.conf import settings



def start(u):
    return  f"""
Install pip install tghandler 

Edit TG\_HANDLER\_CODE setting to  

`{u.code}` 

TG\_HANDLER\_HOST to  

```
{settings.HOST}
```

And add tghandler.TGHandler to the MIDDLEWARE list
            """



def error(data):
    return f"""
Response code: {data.get('res_code')}

```
Reason: {data.get('reason')}
```
Traceback:

```
{data.get('ex_info')}
```
Additional: 

```
{data.get('body')}
```
    """