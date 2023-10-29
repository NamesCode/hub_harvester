{
  description = "Praise be thine AI overlords. Let us feed them thinest data";
  outputs = {
    self,
    nixpkgs,
    flake-utils,
  }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = nixpkgs.legacyPackages.${system};
      in {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            python311
            python311Packages.pygithub
            python311Packages.pprintpp
            python311Packages.sqlite3
            python311Packages.getpass
          ];
        };
      }
    );
}
