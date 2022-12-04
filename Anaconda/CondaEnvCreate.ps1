param([parameter(mandatory=$true)][string]$name)

# Here document without variable expansion
$yml=@'
name: tmpenv
channels:
  - defaults
dependencies:
  - ca-certificates=2022.10.11=haa95532_0
  - certifi=2022.9.24=py37haa95532_0
  - openssl=1.1.1s=h2bbff1b_0
  - pip=22.2.2=py37haa95532_0
  - python=3.7.15=h6244533_0
  - setuptools=65.5.0=py37haa95532_0
  - sqlite=3.40.0=h2bbff1b_0
  - vc=14.2=h21ff451_1
  - vs2015_runtime=14.27.29016=h5e58377_2
  - wheel=0.37.1=pyhd3eb1b0_0
  - wincertstore=0.2=py37haa95532_2
  - pip:
    - cython==0.29.32
    - numpy==1.21.6
#    - git+https://github.com/philferriere/cocoapi.git#egg=pycocotools&subdirectory=PythonAPI

'@

# Create temporary file.yml
$scriptname = $MyInvocation.MyCommand.name
$ts = Get-Date -Format yyyyMMddHHmmss
$tmpyml = $scriptname + ".tmp." + $ts + ".yml"
Write-Output $yml | Out-File $tmpyml -Encoding utf8

try{
    conda env create -f $tmpyml -n $name
    If($LastExitCode -gt 0){
        throw
    }
}catch{
    Write-Error "Exception occurred while conda create -f <internal temporary file> -n $name"
    exit 1
}finally{
    #Delete Temporary Files
    Remove-Item $tmpyml
}

try{
    # Fail to activate causes exception
    conda activate $name
}catch{
    Write-Error "Exception occurred while conda activate $name"
    exit 1
}
Write-Host "Success:conda activate $name"

try{
    #$env:DISTUTILS_USE_SDK=1
    #Write-Host "set DISTUTILS_USE_SDK=$env:DISTUTILS_USE_SDK"
    pip install "git+https://github.com/philferriere/cocoapi.git#egg=pycocotools&subdirectory=PythonAPI"
    If($LastExitCode -gt 0) {throw}
}catch{
    Write-Error "Exception occurred while pip installl"
}

try{
    conda deactivate
}catch{
    Write-Error "Exception occurred while conda deactivate"
    exit 1
}
Write-Host "Success:conda deactivate"
Write-Host "Success:All"
