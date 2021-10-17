run:
	docker build . -t zero-tier-platforms-build:latest
	docker create -ti --rm --name zero-tier-platforms-build zero-tier-platforms-build bash
	docker cp zero-tier-platforms-build:/tmp/ZeroTier-GUI.deb ZeroTier-GUI.deb
	docker cp zero-tier-platforms-build:/tmp/ZeroTier-GUI.rpm ZeroTier-GUI.rpm
	docker rm -f zero-tier-platforms-build
