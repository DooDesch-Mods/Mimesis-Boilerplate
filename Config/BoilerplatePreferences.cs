using System;
using MelonLoader;

namespace Boilerplate.Config
{
	internal static class BoilerplatePreferences
	{
		private const string CategoryId = "Boilerplate";

		private static MelonPreferences_Category? _category;
		private static MelonPreferences_Entry<bool>? _enabled;

		internal static void Initialize()
		{
			if (_category != null)
			{
				return;
			}

			_category = MelonPreferences.CreateCategory(CategoryId, "Boilerplate");
			_enabled = CreateEntry("Enabled", true, "Enabled", "Enable Boilerplate functionality. When disabled, the mod will not modify game behavior.");
		}

		private static MelonPreferences_Entry<T> CreateEntry<T>(string identifier, T defaultValue, string displayName, string? description = null)
		{
			if (_category == null)
			{
				throw new InvalidOperationException("Preference category not initialized.");
			}

			return _category.CreateEntry(identifier, defaultValue, displayName, description);
		}

		internal static bool Enabled => (_enabled ?? throw new InvalidOperationException("Preferences must be initialized before use.")).Value;
	}
}

