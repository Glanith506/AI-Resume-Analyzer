# Docker basics — bundled introductory learning notes
These are project-authored demo notes, not official Docker documentation.

Docker packages an application and its dependencies into a container. An image is a template used to create containers. A container runs an instance of an image. Containers share the host kernel; they are not complete virtual machines with separate kernels.

A Dockerfile describes how to build an image. FROM selects a base image. WORKDIR sets the working directory. COPY copies application files into the image. RUN executes build steps such as installing dependencies. CMD sets the default startup command.

For a beginner Python exercise, create a script that prints a greeting. Use a Python base image, copy the script into the image, and set CMD to run it. Build the image using docker build -t hello-python . and run it using docker run --rm hello-python. These are suggested practice steps, not evidence of experience.

A port mapping connects a host port to a container port. For example, docker run -p 8501:8501 my-streamlit-app maps host port 8501 to container port 8501. The app must listen on 0.0.0.0 inside the container. Do not bake API keys into an image; provide environment variables at runtime.
