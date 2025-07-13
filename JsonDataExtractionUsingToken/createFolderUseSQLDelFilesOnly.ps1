# Server Configurations
$server = 'DESKTOP-GR6FEMK\SQLEXPRESS'
$database = 'TE_3E_PROD'

# Define the SQL query to fetch data
$query = @"
SELECT DISTINCT BC
FROM DummyData
"@

try {
    # Fetch data from the database
    $data = Invoke-Sqlcmd -ServerInstance $server -Database $database -Query $query

    # Define the base path where folders will be created
    $basePath = "C:\Users\abhij\Desktop\distination\powerShellProject"

    # Function to delete only files within folders
    function Remove-FilesInFolder {
        param(
            [string]$folderPath
        )

        # Get all files under the current folder path
        $files = Get-ChildItem -Path $folderPath -File -Force

        # Delete each file and display the file name
        foreach ($file in $files) {
            Write-Host "Deleting file: $($file.FullName)"
            Remove-Item -Path $file.FullName -Force
        }
    }

    # Remove all files under the base path but keep folders
    $folders = Get-ChildItem -Path $basePath -Directory -Force
    foreach ($folder in $folders) {
        Remove-FilesInFolder -folderPath $folder.FullName
    }

    # Loop through the data and create folders
    foreach ($row in $data) {
        $folderName = $row.BC
        $folderPath = Join-Path -Path $basePath -ChildPath $folderName

        # Create the folder if it doesn't exist
        if (-not (Test-Path -Path $folderPath -PathType Container)) {
            New-Item -Path $folderPath -ItemType Directory -Force
            Write-Host "Folder created: $folderPath"
        } else {
            Write-Host "Folder already exists: $folderPath"
        }
    }
} catch {
    Write-Host "An error occurred: $_"
}
