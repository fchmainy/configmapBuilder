#!/usr/bin/env python3
import json
import getopt, sys

def usage():
	print("python addNewApp.py -d <as3_configmap.json> -t <tenantName> -n <appName> -p <poolName> -q <poolFile.json> -e <policyName> -f <policyFile.json> -o <output.json>")
	print("-d       --declaration	JSON File: input AS3 configmap declaration")
	print("-t	--tenant	String: tenant name")
	print("-n	--appName	String: Application Service Name")
	print("-p	--poolName	String: Application Pool Name")
	print("-q	--poolFile	JSON File: pool description file")
	print("-e	--policyName	String: Endpoint Policy name")
	print("-f       --policyFile	JSON File: pool description file")
	print("-o       --output	output AS3 declaration")

# Some cleanup first
def ifExistsPop(d,t,n,p,e, pn):
	d['declaration'][t][n].pop(p, None)
	
	for rule in d['declaration'][t][n][pn]['rules']:
		print(rule['name'])
		if rule['name'] == "forward_to_"+ p:
			#del d['declaration'][t][n][pn]['rules'][i]
			d['declaration'][t][n][pn]['rules'].remove(rule)
	return d

def buildConfigmap(d,t,n,p,q,e,f,pe):
	d['declaration'][t][n][p]=q
	d['declaration'][t][n][pe]['rules'].append(f)

	return d

# Reconciliate entries
def reconciliate(d,t,n,p,q,e,f,o):

	with open(d) as f1:
		data_configmap = json.load(f1)

	with open(q) as f2:
		data_pool = json.load(f2)

	with open(f) as f2:
		data_policy = json.load(f2)

	policyName = data_configmap['declaration'][t][n]['serviceMain']['policyEndpoint']
	clean_CM = ifExistsPop(data_configmap, t, n , p, e, policyName)
	outputFile = buildConfigmap(clean_CM, t, n, p, data_pool, e, data_policy, policyName)

	return outputFile
	

def createFile(o, res):
	with open(o,'w') as f:
		json.dump(res, f)

def main(argv):
	try:
		(opts, args) = getopt.getopt(argv, 'hd:t:n:p:q:e:f:o:', ['help','declaration=','tenant=', 'appName=', 'poolName=', 'poolFile=', 'policyName=', 'policyFile=', 'output='])
	except getopt.GetoptError as err:
		print(err)
		sys.exit(2)

	if len(opts) != 0:
		for (o, a) in opts:
			if o in ('-h', 'h', '--help'):
				usage()
				sys.exit()
			elif o in ('-d', '--declaration'):
                                declaration = a
			elif o in ('-t', '--tenant'):
				tenant = a
			elif o in ('-n', '--appName'):
				appName = a
			elif o in ('-p', '--poolName'):
				poolName = a
			elif o in ('-q', '--poolFile'):
				poolFile = a
			elif o in ('-e', '--policyName'):
				policyName = a
			elif o in ('-f', '--policyFile'):
				policyFile = a
			elif o in ('-o', '--output'):
				output = a
			else:
				usage()
				sys.exit(2)
	else:
		usage()
		sys.exit(2)
	res=reconciliate(declaration, tenant, appName, poolName, poolFile, policyName, policyFile, output)
	createFile(output, res)

if __name__ == '__main__':
	main(sys.argv[1:])

