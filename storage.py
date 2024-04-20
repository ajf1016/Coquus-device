import uos

# Get filesystem information
fs_stat = uos.statvfs('/')

# Calculate total and free space in bytes
total_space = fs_stat[0] * fs_stat[2]
free_space = fs_stat[0] * fs_stat[3]

# Convert bytes to megabytes (1 MB = 1024 * 1024 bytes)
total_space_mb = total_space / (1024 * 1024)
free_space_mb = free_space / (1024 * 1024)

print("Total space: {:.2f} MB".format(total_space_mb))
print("Free space: {:.2f} MB".format(free_space_mb))
