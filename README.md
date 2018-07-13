# Blockchain Python Example


#### Run all the nodes in separate terminals

`python3 node.py`

It will show output as 

> Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)

`python3 node1.py`

It will show output as 

> Running on http://0.0.0.0:5001/ (Press CTRL+C to quit)

`python3 node2.py`

It will show output as 

> Running on http://0.0.0.0:5002/ (Press CTRL+C to quit)

#### Use [Postman](https://www.getpostman.com) to open the urls.

- **[GET]:** **_`/mine`_** to tell our server to mine a new block.
    
- **[GET]:** **_`/chain`_** to return the full Blockchain.
    
- **[POST]:** **_`/transactions/new`_** to create a new transaction to a block

    Post json data sample:
    
    `{
     "sender": "sender_node_address",
     "recipient": "recipient_node_address",
     "amount": 5
    }`
    
- **[POST]:** **_`/nodes/register`_** to accept a list of new nodes in the form of URLs.

    Post json data sample:
    
    `{
        "nodes": ["http://localhost:5001",  "http://localhost:5002"]
    }`
- **[GET]:** **_`/nodes/resolve`_** to implement our Consensus Algorithm, which resolves any conflicts—to ensure a node has the correct chain.

`Blockchain_Example.postman_collection.json` impot it in postman to run post request like **_`/transactions/new`_** or **_`/nodes/register`_**
  
    
Now we have three nodes running on localhost port 5000, 5001 and 5002 respectively. Lets call it node0, node1 and node2.

- **Step 1. Register nodes:** Call the **_`/nodes/register`_** with respective post json data to register {node1, node2} to node0, {node0, node2} to node1, {node0, node1} to node2

- **Step 2. Mine:** Call **_`/mine`_** on any node. Each time you call this api it will mine a block. Remember its your blockchain so feel free to mine as much as you can. 

- **Step 3. Make a Transaction:** Call **_`/transactions/new`_** on the node you mined to make a transaction. To get the address of each node open **_`/`_** on the node and it will show you the amount mined by that node and the address.
 **_When you made all your transaction mine again to make that transaction permanent._**
 
Now you can call **_`/`_** on any node to see the amount or node address or **_`/chain`_** to see all the block chain. You can learn more from the references.

Please let us know in the issue or at `team@litewit.com` if there is any mistakes in implementation or logic. The code was inspired by references as well.


Initial code were taken from references which then were modified a little. 
    
For reference...

[Learn Blockchains by Building One](https://hackernoon.com/learn-blockchains-by-building-one-117428612f46)

[Let’s Build the Tiniest Blockchain](https://medium.com/crypto-currently/lets-build-the-tiniest-blockchain-e70965a248b)

[Let’s Make the Tiniest Blockchain Bigger](https://medium.com/crypto-currently/lets-make-the-tiniest-blockchain-bigger-ac360a328f4d)