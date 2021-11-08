<div align="center">

  <h3 align="center">Movie Data Platform</h3>

  <p align="center">
    This is a big data movie platform for data processing and analysis of IMDb and MovieLens datasets.
    <br />
    <a href="https://moviedataplatform.com/">View Website</a>
  </p>
</div>


### About The Data Flow
<a href="https://moviedataplatform.com/dataFlow">Data Flow</a>


### Technical Details
<a href="https://moviedataplatform.com/behindTheScenes">Behind The Scenes</a>


<!-- GETTING STARTED -->
## Getting Started

This is not a step by step guide, but rather a quick overview of the most important setup of this project.

<p align="left" style="color:red">
Beware the AWS costs when you run the jobs.
</p>

### Data Pipeline Prerequisites

Make sure you have the following prerequisites:

1. Setup the AWS account with the necessary permissions.
2. Setup circleci account.
3. Import the AWS credentials in the circleci Environment Variables.
4. Link the GitHub account with the circleci account.

You can follow the documentation <a href="https://learn.hashicorp.com/tutorials/terraform/circle-ci">here</a>

<p align="right">(<a href="#top">back to top</a>)</p>


### Data Pipeline Deployment

Once you setup the accouts above, you can run the pipeline to deploy the project in circleci.

After the Terraform apply, all the services will be deployed in AWS. You can save the API Gateway URL to use it later.

<p align="right">(<a href="#top">back to top</a>)</p>


### Web Prerequisites and local development

Make sure you have the following prerequisites:

* Update npm to the latest version.
  ```sh
  npm install npm@latest -g
  ```

Go to the src/web folder and run the following commands:

* Install the dependencies:
  ```sh
  npm install
  ```

* Run the server:
  ```sh
  npm start
  ```

You can find the web application at: http://localhost:3000

### Web Deployment

Copy the API Gateway URL from the Terraform output and replace the following line in the src/web/src/Config.js file:

```js
  DATA_API_URL: "{ your_api_gateway_url }",
```

After replacing the URL, run the pipeline to deploy the project in circleci.

You can replace the GA tracking id if you want to use it.

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- ROADMAP -->
## Roadmap

- [] Add cast/crew/director/writer data analysis of IMDb and MovieLens datasets.
- [] Add Rotten Tomatoes dataset.
- [] Add Metacritic dataset.
- [] Multi-language Support
    - [] French
    - [] Japanese
    - [] Chinese
    - [] Spanish

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

I'm a Cloud Data Engineer and Full Stack Web Developer.

You can find me on [LinkedIn](www.linkedin.com/in/joshch1630)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Please find references to the following sources:

* [IMDb Datasets](https://www.imdb.com/interfaces/)
* [MovieLens Datasets](https://grouplens.org/datasets/movielens/)
* [circleci](https://circleci.com/)
* [AWS](https://aws.amazon.com/)
* [Terraform](https://www.terraform.io/)
* [React](https://reactjs.org/)
* [ICONS8](https://icons8.com/)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png