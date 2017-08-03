# uss
A DoSelect Enterprise

[An answer to this quest](https://github.com/doselect/quests/blob/master/backend-developer/image-api.md)

Django project. hosted [here](https://jonny-quest.herokuapp.com/api/v1/ping/) and [Postman Collection](https://www.getpostman.com/collections/c32066d8845bd2442dd2)

#### Description:
* All images are hosted on the disk file in the files folder, as db use isn't allowed. As are the keys (insecure, I know) to get quicker access instead of searching.
* Images are stored in files/<key>/<image_name_with_extension>/ format to make it easier to fetch and create.
* There are two management commands to generate and regenerate keys which are called from the view.
* I have used Function based views as Viewsets can't be used due to lack of a model due to lack of DB usage.
* Utility modules are in modules directory where all the action happens.

#### Assumptions:
* not on prod (duh)
* time constraints are not there (else everything will fail as a 3-4 mb image takes about 15 sec to create due to PIL compression and file write).
* PATCH API will update the whole file to the one updated and not partial update of said image.
* Keys are also generated through api (which calls a management command) for simplicity.
* Data storage format: files/<key>/<image_name_with_extension>/
* A file files/key_list.txt with valid keys (unencrypted for now so as not to increase the time taken), to validate keys and not search the whole directory all the time, as file operations have already made it very slow.


#### APIs:
(Very Slow due to file writes/reads and image sizes)
* [x] POST Key Generation
* [x] PUT Key regeneration (invalidate old key)
* [x] GET list of key's images
* [x] GET image (by name)
* [x] POST image (creation)
* [x] PATCH image (update image by name)
* [x] DELETE image (delete image by name)

#### TODO:
* [x] image compression (PIL? or gzip? time offsets?)
Used PIL for now, makes it very slow. possibly shoot an event which some service can pick up asynchronously
