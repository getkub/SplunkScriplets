# Stitch documents with Javascript & CSS 
# Pre-req: marked.js , strapdown.js , strapdown.css, jquery.js, themes
# Present working directory where script is running
function Get-ScriptDirectory
{
  $Invocation = (Get-Variable MyInvocation -Scope 1).Value
  Split-Path $Invocation.MyCommand.Path
}

# If specific Rule book has to be created
# $ruleBookName = Read-Host 'Input rulebook:'
$scriptDir = Get-ScriptDirectory

# ------------------------------------------------------------
# All items are considered relative to $scriptDir
# ------------------------------------------------------------
$baseDir=(get-item $scriptDir ).parent.FullName
Set-Location -Path $baseDir

$ruleDir=$baseDir + "\rules\"
$taskDir=$baseDir + "\tasks\"
$templateDir=$baseDir + "\template\"
$outputDir=$baseDir + "\output\"
$outputDirJS=$baseDir + "\output\lib\"
$outputDirCSS=$baseDir + "\output\lib\themes"
$jsCSSFile=$templateDir + "\js_css.mash"



# Cleanup Output directory for any previous outputs
Remove-Item $outputDir\combined_play*.html



# Get All Rule books from the $ruleBook location
# Updated Filter to look only for playbooks
foreach($file in Get-ChildItem $ruleDir -Filter combined_play*.txt)
{
	$ruleBookName= [io.path]::GetFileNameWithoutExtension($file)
	#Output file will have RuleBookName in its name
	$outputFile= $outputDir + $ruleBookName + ".html"

	Write-Host "$(Get-Date -format 'u') Start Creating Book ("$ruleBookName") ..."
	$ruleBookPath = $ruleDir + $file
	# Now iterate all tasks in playbook and avoid any lines starting with # or empty lines
	Try
	{
		$ruleBookContent= Get-Content $ruleBookPath -ErrorAction Stop | select-string -notmatch  "^\s*#|^\s*$"
	}
	Catch
	{
		$ErrorMessage = $_.Exception.Message
		$FailedItem = $_.Exception.ItemName
		Write-Host "Error occured for Item Name:" $FailedItem "::" "Error Message:" $ErrorMessage
		Break
	}

	# ------------------------------------------------------------
	# Read the contents of the ruleBook one by one
	# Then concatenate all the files
	# ------------------------------------------------------------
	$htmlHeaderFile1=$templateDir + "html_header1.txt"
	Try
	{
		Get-Content $htmlHeaderFile1 | Out-File -encoding ascii -filepath $outputFile
		Get-Content $ruleBookContent | Out-File -encoding ascii -Append -filepath $outputFile
		Get-Content $jsCSSFile       | Out-File -encoding ascii -Append -filepath $outputFile
	}
	Catch
	{
		$ErrorMessage = $_.Exception.Message
		$FailedItem = $_.Exception.ItemName
		Write-Host "Error occured for Item Name:" $FailedItem "::" "Error Message:" $ErrorMessage
		Break
	}
	Write-Host "$(Get-Date -format 'u') Finished Creating Book ("$ruleBookName") ..."
}
# Now go back to original where you started running the script
Set-Location -Path $scriptDir
