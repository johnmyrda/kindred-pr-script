# Fetch Open Pull Requests

The script pull-request-age.py returns the open pull requests for a github repo using the GitHub v3 REST API.

## How to use

Python 3 is required to run the script.

Run the script followed by the repo in the [user]/[repo] format e.g. apple/swift:

```
./pull-request-age.py repo
```

## Example

```
$ ./pull-request-age.py google/filament
Open pull requests for the google/filament repository
See online at https://www.github.com/google/filament/pulls
Name: Suzanne now uses LINEAR_MIPMAP_LINEAR.
Age: 4 hours, 52 minutes

Name: don’t leak the ExternalContext object
Age: 6 hours, 6 minutes

Name: Fix utils::Path concat for relative paths.
Age: 6 hours, 7 minutes

Name: Add a few new nodes to Tungsten
Age: 1 day, 14 hours
```

## JSON Output

If you need the response in JSON format as described at https://developer.github.com/v3/pulls/#response use the optional `--output-json` flag.
