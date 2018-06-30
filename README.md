# Blockchain Python Example


###Run all the nodes in separate terminals

`python3 node.py`

It will show output as 

> Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)

`python3 node1.py`

It will show output as 

> Running on http://0.0.0.0:5001/ (Press CTRL+C to quit)

`python3 node2.py`

It will show output as 

> Running on http://0.0.0.0:5002/ (Press CTRL+C to quit)

###Use [Postman](https://www.getpostman.com) to open the urls.

- **[GET]:** **_`/mine`_** to tell our server to mine a new block.
    
- **[GET]:** **_`/chain`_** to return the full Blockchain.
    
- **[POST]:** **_`/transactions/new`_** to create a new transaction to a block

    Post json data sample:
    
    `{
     "sender": "128963cb75c74fdfa60068e426577985",
     "recipient": "128963cb75c74fdfa60068e426577986",
     "amount": 5
    }`
    
- **[POST]:** **_`/nodes/register`_** to accept a list of new nodes in the form of URLs.

    Post json data sample:
    
    `{
        "nodes": ["http://localhost:5001",  "http://localhost:5002"]
    }`
- **[GET]:** **_`/nodes/resolve`_** to implement our Consensus Algorithm, which resolves any conflicts—to ensure a node has the correct chain.
    
Now we have three nodes running on localhost port 5000, 5001 and 5002 respectively. Lets call it node0, node1 and node2.

Call the **_`/nodes/register`_** with respective post json data to register {node1, node2} to node0, {node0, node2} to node1, {node0, node1} to node2

**_Now select your favorite node and start mining._** Call **_`/mine`_** on that node. Each time you call this api it will mine a block.

Remember its your blockchain so feel free to mine as much as you can. When you are done, call the **_`/nodes/resolve`_** on each node to update the chain by resolving the conflict.  

Call the **_`/chain`_** api on each node to see the blockchain. You will find all nodes have the same block chain.


You can mine from other nodes as well. Make sure to resolve the nodes.


    
For reference...

[Learn Blockchains by Building One](https://hackernoon.com/learn-blockchains-by-building-one-117428612f46)

[Let’s Build the Tiniest Blockchain](https://medium.com/crypto-currently/lets-build-the-tiniest-blockchain-e70965a248b)

[Let’s Make the Tiniest Blockchain Bigger](https://medium.com/crypto-currently/lets-make-the-tiniest-blockchain-bigger-ac360a328f4d)