import harmat as hm

# initialise the harm
h = hm.Harm()

# create the top layer of the harm
# top_layer refers to the top layer of the harm
h.top_layer = hm.AttackGraph()

# we will create 5 nodes and connect them in some way
# first we create some nodes
hosts = [hm.Host("Host {}".format(i)) for i in range(4)]
# then we will make a basic attack tree for each
for host in hosts:
    host.lower_layer = hm.AttackTree()
    # We will make two vulnerabilities and give some metrics
    vulnerability1 = hm.Vulnerability('CVE-0000', values = {
        'risk' : 9,
        'cost' : 4,
        'probability' : 0.2,
        'impact' : 12
    })
    vulnerability2 = hm.Vulnerability('CVE-0001', values = {
        'risk' : 1,
        'cost' : 5,
        'probability' : 0.2,
        'impact' : 2
    })
    # basic_at creates just one OR gate and puts all vulnerabilites
    # the children nodes
    host.lower_layer.basic_at([vulnerability1, vulnerability2])
    
# Now we will create an Attacker. This is not a physical node but it exists to describe
# the potential entry points of attackers.
attacker = hm.Attacker() 

# To add edges we simply use the add_edge function
# here h[0] refers to the top layer
# add_edge(A,B) creates a uni-directional from A -> B.
h[0].add_edge(attacker, hosts[0]) 
h[0].add_edge(hosts[0], hosts[3])
h[0].add_edge(hosts[1], hosts[0])
h[0].add_edge(hosts[0], hosts[2])
h[0].add_edge(hosts[3], hosts[2])


# Now we set the attacker and target
h[0].source = attacker
h[0].target = hosts[3]

# do some flow up
h.flowup()

# Now we will run some metrics
hm.HarmSummary(h).show()

file = open("example.txt", "w")
file.write(str(h.risk) + "\n")
file.write(str(h.cost) + "\n")
file.write(str(h[0].mean_path_length()) + "\n")
file.write(str(h[0].mode_path_length()) + "\n")
file.write(str(h[0].shortest_path_length()) + "\n")
file.write(str(h[0].return_on_attack()) + "\n")
file.write(str(h[0].probability_attack_success()) + "\n")
file.close()

