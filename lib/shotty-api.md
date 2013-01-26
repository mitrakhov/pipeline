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
````
project = api.project.get(slug='TST')
````
json output
````
{
meta: {
limit: 1000,
next: null,
offset: 0,
previous: null,
total_count: 1
},
objects: [
{
description: "",
director: "Anton Mitrakhov",
end_date: null,
id: 2,
kind: "0",
name: "Test",
poster: "/files/posters/post-85785-1345161467_1.jpg",
pub_date: "2013-01-09T18:39:22",
resource_uri: "/api/v1/project/2/",
slug: "TST",
start_date: null
}
]
}
````



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
