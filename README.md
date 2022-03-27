
# Building Microservice Communication With RabbitMQ

* This project demonstrates the implementation of three microservice applications whose interservice communication is handled by rabbitmq.
* All the microservices are dockerized and are run in containers as isolated applications.


## Workflow

* Based on the dependencies mentioned in the yml file, docker images are built and containers are up and running.
### Producer

* A ride request is sent to producer containing the details about the ride such as pickup, destination and so on.
* Producer has a list of all the consumers which are currently available and maps each request to one of the consumers randomly.
* A rabbitmq queue is declared for each of these consumers to which the details about the ride and its corresponding matched consumer is pushed.

### Consumer

* Every time a consumer service starts it reads consumer id and ip address from environment variable and sends the details as a post request to producer.
* The details are stored in the producer in a list. In addition to sending post requests, the consumer also constantly consumes data from the queue to which the details about the ride are pushed. 
* The data recieved is printed.

### Database

* In the producer along with the dedicated queue for a consumer, an additional queue is declared which is a global queue named database queue. 
* The ride details and its matched consumer are pushed to this queue. 
* In database microservice we access the details present in this queue and insert it into mongodb. 
* Mongodb host and collection are created beforehand.




## Team Members:
- PES1UG19CS519: Sumukh Raju Bhat
- PES1UG19CS469: Shreyas Vinayaka Basri KS
- PES1UG19CS525: Surya M N
- PES1UG19CS514: Suhas R K
