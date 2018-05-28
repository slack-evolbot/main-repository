import disp_util

test = []
test.append(" 1    <1 ms    <1 ms    <1 ms  192.168.0.16")
test.append(" 2    <1 ms     1 ms    <1 ms  210.150.XXX.XXX")
test.append(" 3     2 ms     1 ms     2 ms  210.153.XXX.XXX")
test.append(" 4     4 ms     2 ms     1 ms  210.153.XXX.XXX")
test.append("20     *        *        *     Request timed out.")
test.append("21     *        *        *     Request timed out.")
test.append("22     *        *        *     Request timed out.")
test.append("23     *        *        *     Request timed out.")

counter = 1
bef_resp = ''
for resp in test:
    print(str(counter) + ":" + resp)
    counter += 1

    if resp.find("Request timed out") != -1:
        disp_util.print_disp_flowing_ex(bef_resp)
        break

    bef_resp = resp
