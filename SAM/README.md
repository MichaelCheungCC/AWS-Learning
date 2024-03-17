## SAM Learning
API Gateway > Lambda > DynamoDB

### Setup
1. Follow the *command.sh* file
2. Add ID as primary key on DynamoDB
3. Create item with ID=1

#### Get
Query String
```json
ID=1
```
#### POST
Request body
```json
{
  "Item": "{\"ID\": {\"S\": \"5\"}, \"Age\": {\"N\": \"29\"}, \"Name\": {\"S\": \"Teddy\"}}"
}
```
#### DELETE
Request body
```json
{
  "Item": "{\"ID\": {\"S\": \"6\"}}"
}
```