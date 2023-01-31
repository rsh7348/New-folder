resource "local_file" "test1" {
    filename = "/tmp/terratest.txt"
    content = " This is test file creation"
    file_permission = "644"
}