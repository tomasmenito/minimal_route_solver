test:
	poetry run pytest -sx


build-image:
	docker build -t minimal_route_solver:latest .


sample-docker:
	docker run -v $(pwd)/samples:/shared minimal_route_solver:latest /shared/cargo.csv /shared/trucks.csv /shared/response.csv
