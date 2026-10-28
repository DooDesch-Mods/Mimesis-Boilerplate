using Boilerplate.Config;
using MelonLoader;

[assembly: MelonInfo(typeof(Boilerplate.Core), "Boilerplate", DooDesch.ModVersion.Current, "DooDesch", null)]
[assembly: MelonGame("ReLUGames", "MIMESIS")]

namespace Boilerplate
{
	public sealed class Core : MelonMod
	{
		public override void OnInitializeMelon()
		{
			BoilerplatePreferences.Initialize();
			// MelonLoader applies this assembly's Harmony patches after initialization.
			MelonLogger.Msg("Boilerplate initialized. Enabled={0}", BoilerplatePreferences.Enabled);
		}
	}
}

