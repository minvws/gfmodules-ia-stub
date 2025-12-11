# I&A Stub

This app is the I&A Stub and is part of
the 'Generieke Functies, lokalisatie en addressering' project of the Ministry of Health, Welfare and Sport of the Dutch government.

## Disclaimer

This project and all associated code serve solely as documentation
and demonstration purposes to illustrate potential system
communication patterns and architectures.

This codebase:

- Is NOT intended for production use
- Does NOT represent a final specification
- Should NOT be considered feature-complete or secure
- May contain errors, omissions, or oversimplified implementations
- Has NOT been tested or hardened for real-world scenarios

The code examples are only meant to help understand concepts and demonstrate possibilities.

By using or referencing this code, you acknowledge that you do so at your own
risk and that the authors assume no liability for any consequences of its use.

## Enable SSH agent forwarding

At this point, the MAX Core framework a git-type dependency, because is it not
yet available as a Python package. Installing this dependency in the Docker
environment requires a SSH key for authentication. To enable this scenario,
follow the steps below to automatically forward your local SSH agent if one is
running.

```sh
# Example:
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519   # or your key path
ssh-add -l                  # verify key is loaded
```

Note that on macOS, the above `eval` command is not needed. Just make sure to
add the key to your path, every time the host machine is restarted.

Further information can be found in the
[VS Code docs](https://code.visualstudio.com/remote/advancedcontainers/sharing-git-credentials).

## Contribution

As stated in the [Disclaimer](#disclaimer) this project and all associated code serve solely as documentation and
demonstration purposes to illustrate potential system communication patterns and architectures.

For that reason we will only accept contributions that fit this goal. We do appreciate any effort from the
community, but because our time is limited it is possible that your PR or issue is closed without a full justification.

If you plan to make non-trivial changes, we recommend to open an issue beforehand where we can discuss your planned changes.
This increases the chance that we might be able to use your contribution (or it avoids doing work if there are reasons why we wouldn't be able to use it).

Note that all commits should be signed using a gpg key.
