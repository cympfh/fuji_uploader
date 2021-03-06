# Fuji Uploader

## Directory/File Tree

```
- ${ROOT}/
  - 101_FUJI/
    + DSCF1001.JPG
    + DSCF1001.RAF
    + DSCF1xxx.*
  - 102_FUJI/
    + DSCF2xxx.*
  - :
  - 109_FUJI/
    + DSCF9xxx.*
  - 110_FUJI/
    + DSCF0xxx.* <- The number returns back!
```

The file name `DSCFxxxx.*` be generated by Fuji-camera.
And this system 

## APIs

### FileExists

`GET /exists/<filename>`

`<filename>` is like `DSCF1002.JPG`.
The response is `Yes` with status code `200` if exists, else `No` with status code `404`.

*NOTE*: This API checks whether any file with the `filename` exists in the **latest 9,999** images.
(This is because the name duplicates every 10,000 images.)

### Upload

`POST /upload/<filename>`

POST body must be the file content.

Save the body as `filename`.
To avoid overwrite, find (or create) the fresh directory.
