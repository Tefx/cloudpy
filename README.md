cloudpy
=======

run python script in virtual environment on a remote platform


# Install
    $pip install cloudpy
    
# Usage
## The easy way
    $cloudpy your_script
## The hard way
    $cloudpy -P your_script
You can do some modifications to the packed structure here

    $cloudpy -S your_package_name
Send to remote host. The package name has been return by "-P" command

    $cloudpy -R your_package_name
Run!
    
    $cloudpy -C your_package_name
Clean.