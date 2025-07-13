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

    # Function to recursively delete folders and their files
    function Remove-FolderContents {
        param(
            [string]$folderPath
        )

        # Get all files and folders under the current folder path
        $items = Get-ChildItem -Path $folderPath -Force

        # Recursively delete each item
        foreach ($item in $items) {
            if ($item.PSIsContainer) {
                Remove-FolderContents -folderPath $item.FullName
            } else {
                Remove-Item -Path $item.FullName -Force
            }
        }

        # Remove the current folder
        Remove-Item -Path $folderPath -Force
    }

    # Remove all folders and files under the base path
    Remove-FolderContents -folderPath $basePath

    # Loop through the data and create folders
    foreach ($row in $data) {
        $folderName = $row.BC
        $folderPath = Join-Path -Path $basePath -ChildPath $folderName

        # Create the folder
        New-Item -Path $folderPath -ItemType Directory -Force
        Write-Host "Folder created: $folderPath"
    }
} catch {
    Write-Host "An error occurred: $_"
}
