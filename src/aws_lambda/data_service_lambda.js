const AWS = require("aws-sdk");

const dynamo = new AWS.DynamoDB.DocumentClient();

exports.handler = async (event, context) => {

  let body;
  let statusCode = 200;

  // Testing
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST,PUT,GET,OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type,Access-Control-Allow-Headers,Authorization,X-Requested-With'
  };

  try {
    switch (event.httpMethod + " " + event.resource) {

      case "GET /data/{dataTitle}":
        body = await dynamo
          .get({
            TableName: "mdp_data_analysis",
            Key: {
              data_title: event.pathParameters.dataTitle
            }
          })
          .promise();
        break;

      case "GET /comment/{sectionId}":
        body = await dynamo
          .query({
            TableName: "mdp_comment",
            KeyConditionExpression: "#sectionId = :sectionId",
            FilterExpression: "#isDelete = :isDelete",
            ExpressionAttributeNames: {
              "#sectionId": "sectionId",
              "#isDelete": "isDelete",
            },
            ExpressionAttributeValues: {
              ":sectionId": event.pathParameters.sectionId,
              ":isDelete": false,
            },
            ScanIndexForward: false,
          })
          .promise();
        break;

      case "POST /comment":
        let requestJSON = JSON.parse(event.body);
        let sectionId = requestJSON.sectionId;
        let name = requestJSON.name;
        let content = requestJSON.content;

        if (sectionId == null || sectionId === ''
          || name == null || name === ''
          || content == null || content === '') {
          throw new Error(`Missing input comment data`);
        }

        let now = Date.now();
        let randomStr = (Math.random() + 1).toString(36).substring(2);
        commentId = now + "_" + randomStr;

        let date = new Date();
        let createDate =
          date.getFullYear() + "/"
          + ("00" + (date.getMonth() + 1)).slice(-2)
          + "/" + ("00" + date.getDate()).slice(-2) + " "
          + ("00" + date.getHours()).slice(-2) + ":"
          + ("00" + date.getMinutes()).slice(-2)
          + ":" + ("00" + date.getSeconds()).slice(-2);

        if (commentId.length > 50
          || sectionId.length > 50
          || name.length > 20
          || createDate.length > 50
          || content.length > 1500) {
          throw new Error(`Exceed maximum string lenght`);
        }

        await dynamo
          .put({
            TableName: "mdp_comment",
            Item: {
              'commentId': commentId,
              'sectionId': sectionId,
              'name': name,
              'createDate': createDate,
              'content': content,
              isDelete: false
            }
          })
          .promise();
        body = `POST item $${requestJSON.commentId}`;
        break;

      default:
        throw new Error(`Unsupported route: "$${event.httpMethod + " " + event.resource}"`);
    }
  } catch (err) {
    statusCode = 400;
    body = err.message;
  } finally {
    body = JSON.stringify(body);
  }

  return {
    statusCode,
    body,
    headers
  };
};