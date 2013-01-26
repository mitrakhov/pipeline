# API examples (create read update delete)


## Dependencies
Required:
* [Slumber](https://github.com/dstufft/slumber)

````
easy_install slumber
````

## Quickstart

````
url = 'http://chimney.shotty.cc/api/v1/'
api = slumber.API(url, auth=('shotty', 'chimney'))
````

### Get project by short name
project = api.project.get(slug='TST')

### Create Sequence for project
````
data = {
  'name': 'FOO',
	'description': 'Foo shots',
	'bid': '',
	'project': str(project['objects'][0]['resource_uri'])
}

api.sequence.post(data)

````
