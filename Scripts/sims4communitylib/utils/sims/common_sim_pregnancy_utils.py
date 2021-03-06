"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union
from sims.pregnancy.pregnancy_tracker import PregnancyTracker
from sims.sim_info import SimInfo
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils
from sims4communitylib.enums.statistics_enum import CommonStatisticId
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
from sims4communitylib.utils.sims.common_sim_statistic_utils import CommonSimStatisticUtils


class CommonSimPregnancyUtils:
    """ Utilities for manipulating the pregnancy status of Sims. """
    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=False)
    def is_pregnant(sim_info: SimInfo) -> bool:
        """ Determine if the specified Sim is pregnant. """
        pregnancy_tracker = CommonSimPregnancyUtils._get_pregnancy_tracker(sim_info)
        if pregnancy_tracker is None:
            return False
        return pregnancy_tracker.is_pregnant

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=False)
    def start_pregnancy(sim_info: SimInfo, partner_sim_info: SimInfo) -> bool:
        """ Start a pregnancy between a Sim and a Partner Sim. """
        if not CommonHouseholdUtils.has_free_household_slots(sim_info):
            return False
        pregnancy_tracker = CommonSimPregnancyUtils._get_pregnancy_tracker(sim_info)
        if pregnancy_tracker is None:
            return False
        pregnancy_tracker.start_pregnancy(sim_info, partner_sim_info)
        pregnancy_tracker.clear_pregnancy_visuals()
        CommonSimStatisticUtils.set_statistic_value(sim_info, CommonStatisticId.PREGNANCY, 1.0)
        return True

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=False)
    def clear_pregnancy(sim_info: SimInfo) -> bool:
        """ Clear the pregnancy status of a Sim. """
        pregnancy_tracker = CommonSimPregnancyUtils._get_pregnancy_tracker(sim_info)
        if pregnancy_tracker is None:
            return False
        sim_info.pregnancy_tracker.clear_pregnancy()
        CommonSimStatisticUtils.remove_statistic(sim_info, CommonStatisticId.PREGNANCY)
        return True

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=False)
    def can_be_impregnated(sim_info: SimInfo) -> bool:
        """ Determine if a Sim can be impregnated. """
        from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
        from sims4communitylib.enums.traits_enum import CommonTraitId
        if CommonSpeciesUtils.is_human(sim_info):
            if CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED):
                return False
            return CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED)
        elif CommonSpeciesUtils.is_pet(sim_info):
            if CommonTraitUtils.has_trait(sim_info, CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_NOT_REPRODUCE):
                return False
            return CommonTraitUtils.has_trait(sim_info, CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_REPRODUCE)
        return False

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=False)
    def can_impregnate(sim_info: SimInfo) -> bool:
        """ Determine if a Sim can impregnate other sims. """
        from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
        from sims4communitylib.enums.traits_enum import CommonTraitId
        if CommonSpeciesUtils.is_human(sim_info):
            if CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE):
                return False
            return CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE)
        elif CommonSpeciesUtils.is_pet(sim_info):
            if CommonTraitUtils.has_trait(sim_info, CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_NOT_REPRODUCE):
                return False
            return CommonTraitUtils.has_trait(sim_info, CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_REPRODUCE)
        return False

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=None)
    def get_partner_of_pregnant_sim(sim_info: SimInfo) -> Union[SimInfo, None]:
        """ Retrieve a SimInfo object of the Sim that impregnated the specified Sim. """
        pregnancy_tracker = CommonSimPregnancyUtils._get_pregnancy_tracker(sim_info)
        if pregnancy_tracker is None:
            return None
        return pregnancy_tracker.get_partner()

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=0.0)
    def get_pregnancy_progress(sim_info: SimInfo) -> float:
        """ Retrieve the pregnancy progress of a Sim. """
        pregnancy_tracker = CommonSimPregnancyUtils._get_pregnancy_tracker(sim_info)
        if pregnancy_tracker is None or not CommonSimPregnancyUtils.is_pregnant(sim_info):
            return 0.0
        pregnancy_commodity_type = pregnancy_tracker.PREGNANCY_COMMODITY_MAP.get(CommonSpeciesUtils.get_species(sim_info))
        statistic_tracker = sim_info.get_tracker(pregnancy_commodity_type)
        pregnancy_commodity = statistic_tracker.get_statistic(pregnancy_commodity_type, add=False)
        if not pregnancy_commodity:
            return 0.0
        return pregnancy_commodity.get_value()

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=0.0)
    def get_pregnancy_rate(sim_info: SimInfo) -> float:
        """ Retrieve the rate at which pregnancy progresses. """
        pregnancy_tracker = CommonSimPregnancyUtils._get_pregnancy_tracker(sim_info)
        if pregnancy_tracker is None:
            return 0.0
        return pregnancy_tracker.PREGNANCY_RATE

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=None)
    def _get_pregnancy_tracker(sim_info: SimInfo) -> Union[PregnancyTracker, None]:
        if sim_info is None:
            return None
        return sim_info.pregnancy_tracker
