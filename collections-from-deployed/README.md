<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>





<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/PaloAltoNetworks/pcs-platform-helper-scripts/collections-from-deployed">
   
  </a>

<h3 align="center">Create Collections from Deployed Container Images</h3>

  <p align="center">
    This project will query the deployed container images and create matching collections based on the uniques cluster and namespace combinations. 
    <br />
    <a href="https://github.com/PaloAltoNetworks/pcs-platform-helper-scripts"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/PaloAltoNetworks/pcs-platform-helper-scripts">View Demo</a>
    ·
    <a href="https://github.com/PaloAltoNetworks/pcs-platform-helper-scripts/issues">Report Bug</a>
    ·
    <a href="https://github.com/PaloAltoNetworks/pcs-platform-helper-scripts/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* python - Create a virtual environment
  ```sh
  python3 -m venv env
  source env/bin/activate
  pip install requests json
  ```

### Installation


1. Clone the repo
   ```sh
   git clone https://github.com/PaloAltoNetworks/pcs-platform-helper-scripts.git
   ```

2. Create a credential file in `~/.prismacloud/credentials.json`
   ```json
   {
    "name":     "App0",
    "url":      "app0.cloud.twistlock.com/app0-xxxxxx",
    "identity": "",
    "secret":   ""
   }
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

To create collections

   ```sh
   python collections-from-deployed.py -c -x credentials.json
   ```


To remove collections

   ```sh
   python remove-created-collections.py -x credentials.json
   ```
 
<p align="right">(<a href="#readme-top">back to top</a>)</p>





<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>







