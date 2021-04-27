# This is an example PKGBUILD file. Use this as a start to creating your own,
# and remove these comments. For more information, see 'man PKGBUILD'.
# NOTE: Please fill out the license field for your package! If it is unknown,
# then please put 'unknown'.

# Maintainer: Tomás Ralph <tomasralph2000@gmail.com>
pkgname=zerotier-gui-git
pkgver=1.2.2
pkgrel=1
pkgdesc="A Linux front-end for ZeroTier"
arch=(any)
url="https://github.com/tralph3/ZeroTier-GUI.git"
license=('GPL3')
depends=(tk python polkit)
makedepends=(git)
optdepends=('zerotier-one: Provides the backend of the program')
source=("git+$url")
md5sums=('SKIP')

pkgver() {
	cd "${_pkgname}"
	prinf "1.2.2.r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
}

package() {
	cd "ZeroTier-GUI"
	chmod +x INSTALL
	./INSTALL
}
