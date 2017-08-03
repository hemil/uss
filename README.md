# uss
A DoSelect Enterprise

[An answer to this quest](https://github.com/doselect/quests/blob/master/backend-developer/image-api.md)

Django project. hosted [here](Not yet)
#### Description:
* All images are hosted on the disk file in the files folder, as db use isn't allowed. As are the keys (insecure, I know) to get quicker access instead of searching.
* Images are stored in files/<key>/<image_name_with_extension>/ format to make it easier to fetch and create.
* There are two management commands to generate and regenerate keys which are called from the view.
* I have used Function based views as Viewsets can't be used due to lack of a model due to lack of DB usage.
* Utility modules are in modules directory where all the action happens.

#### APIs:
* [x] POST Key Generation
* [x] PUT Key regeneration (invalidate old key)
* [x] GET list of key's images
* [x] GET image (by name)
* [x] POST image (creation)
* [ ] PATCH image (update image by name)
* [ ] DELETE image (delete image by name)
