# Edmunds API Python Wrapper Examples

Note: before running any of the examples, be sure to [register for a key](http://edmunds.mashery.com/member/register/) and insert it into the code when the Edmunds class is instantiated: `Edmunds('YOUR API KEY')`.

## Contents
1. [Media: Photos Example](#1-media-photos)
2. [Spec: Make Example](#2-spec-make)

### 1. Media: Photos

This example has two functions, `get_style_id` which returns a style ID for a given make, model, and year,
and `get_photos` which returns a dict of lists of photo URLs for a given style ID. 
The main function is an example of getting photos for the 2013 Tesla Model S.
The endpoints used in this example are [Get Style Details For a Car Make/Model/Year](http://developer.edmunds.com/api-documentation/vehicle/spec_model_year/v2/02_year_details/api-description.html) and 
[Media: Photos](http://developer.edmunds.com/api-documentation/vehicle/media_photos/v1/index.html).

#### Usage
```python
>>> python media_photos.py
{(u'exterior', u'FBDG'): 
  [u'http://media.ed.edmunds-media.com/tesla/model-s/2012/oem/2012_tesla_model-s_sedan_signature_fbdg_oem_2_396.jpg', u'http://media.ed.edmunds-media.com/tesla/model-s/2012/oem/2012_tesla_model-s_sedan_signature_fbdg_oem_2_87.jpg', ..., u'http://media.ed.edmunds-media.com/tesla/model-s/2012/oem/2012_tesla_model-s_sedan_signature_fbdg_oem_2_131.jpg'],
 (u'exterior', u'FQ'): 
  [u'http://media.ed.edmunds-media.com/tesla/model-s/2012/oem/2012_tesla_model-s_sedan_signature_fq_oem_17_300.jpg', u'http://media.ed.edmunds-media.com/tesla/model-s/2012/oem/2012_tesla_model-s_sedan_signature_fq_oem_17_175.jpg', ..., u'http://media.ed.edmunds-media.com/tesla/model-s/2012/oem/2012_tesla_model-s_sedan_signature_fq_oem_18_2048.jpg'],
 ...
}
```
Note: '...' indicates more data removed here clarity & conciseness.

### 2. Spec: Make

This example has one function, `get_makes` which takes three optional parameters (`year`, `state`, and `view`) and returns the JSON response object of the list of makes. The example below is showing the *2013 new* makes, but any `year` and/or `state` can be swapped in. The endpoint used in this example is [Get List of Car Makes](http://developer.edmunds.com/api-documentation/vehicle/spec_make/v2/01_list_of_makes/api-description.html).

#### Usage

```python
>>> python spec_make.py
{u'makesCount': 42, 
 u'makes': [
   {u'models': [
     {u'years': [{u'id': 100538929, u'year': 2013}], u'id': u'Acura_ILX', u'niceName': u'ilx', u'name': u'ILX'},
     {u'years': [{u'id': 200434553, u'year': 2013}], u'id': u'Acura_MDX', u'niceName': u'mdx', u'name': u'MDX'},
     {u'years': [{u'id': 100538949, u'year': 2013}], u'id': u'Acura_RDX', u'niceName': u'rdx', u'name': u'RDX'},
     {u'years': [{u'id': 200433190, u'year': 2013}], u'id': u'Acura_TL', u'niceName': u'tl', u'name': u'TL'}, {u'years':
     [{u'id': 200437325, u'year': 2013}], u'id': u'Acura_TSX', u'niceName': u'tsx', u'name': u'TSX'}, {u'years':
     [{u'id': 200440520, u'year': 2013}], u'id': u'Acura_TSX_Sport_Wagon', u'niceName': u'tsx-sport-wagon', u'name':
     u'TSX Sport Wagon'}, {u'years': [{u'id': 200441835, u'year': 2013}], u'id': u'Acura_ZDX', u'niceName': u'zdx',
     u'name': u'ZDX'}
    ], 
    u'id': 200002038, 
    u'niceName': u'acura', 
    u'name': u'Acura'},
    ...
 ]
}
