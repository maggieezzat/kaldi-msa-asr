checksum_local_file = 'waves_checksum_local.txt'
checksum_remote_file = 'waves_checksum_azure.txt'
diff_file = 'final_waves_diff.txt'

local_sums = {}

with open(checksum_local_file, 'r') as local:
    for line in local:
        local_ch = line.strip().split(',')[1].strip()
        fname = line.strip().split(',')[0].strip().split('/')[-1]
        local_sums[fname] = local_ch


    
    
with open(checksum_remote_file, 'r') as remote:
    with open(diff_file, 'w') as out:
        for line in remote:
            remote_ch = line.strip().split(',')[1].strip()
            fname = line.strip().split(',')[0].strip().split('/')[-1]
            local_ch = local_sums[fname] 
            if local_ch != remote_ch:
                out.write(fname + " " + local_ch + " " + remote_ch + '\n')
        out.write("EOF")
